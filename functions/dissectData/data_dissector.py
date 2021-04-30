import json

from dataclasses import dataclass

import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp

tfd = tfp.distributions
tfb = tfp.bijectors


@dataclass
class SwitchpointTrio:
    switchpoint: int
    pre_switch_average: int
    post_switch_average: int


class DataDissector:
    @classmethod
    def dissect_data(cls, data: list) -> SwitchpointTrio:
        samples_trio = cls.sample(np.array(data))
        [s, m1, m2] = [samples.mean() for samples in samples_trio]
        
        return SwitchpointTrio(
            switchpoint=int(round(s)),
            pre_switch_average=int(round(m1)),
            post_switch_average=int(round(m2)),
        )
        
    @classmethod
    def get_model(cls, count_data):
        timeperiod_length = len(count_data)

        return tfd.JointDistributionNamed(
            dict(
                s=tfd.Uniform(0., timeperiod_length),
                m1=tfd.Exponential(tf.cast(1./count_data.mean(), tf.float32)),
                m2=tfd.Exponential(tf.cast(1./count_data.mean(), tf.float32)),
                c_t=lambda s, m1, m2: tfd.Independent(
                    tfd.Poisson(tf.where(np.arange(timeperiod_length) < s, m1, m2)),
                    reinterpreted_batch_ndims=1,
                ),
        ))


    @classmethod
    def target_log_prob_fn(cls, s, m1, m2, count_data):
        return cls.get_model(count_data).log_prob(s=s, m1=m1, m2=m2, c_t=count_data)


    @classmethod
    @tf.function(autograph=False, experimental_compile=True)
    def make_chain(cls, target_log_prob_fn, timeperiod_length):
        kernel = tfp.mcmc.TransformedTransitionKernel(
            inner_kernel=tfp.mcmc.HamiltonianMonteCarlo(
                target_log_prob_fn=target_log_prob_fn,
                step_size=0.05,
                num_leapfrog_steps=3,
            ),
            bijector=[
                tfb.Sigmoid(low=0., high=tf.cast(timeperiod_length, dtype=tf.float32)),
                tfb.Softplus(),
                tfb.Softplus(),
            ],
        )

        kernel = tfp.mcmc.SimpleStepSizeAdaptation(
            inner_kernel=kernel,
            num_adaptation_steps=2000,
        )

        states = tfp.mcmc.sample_chain(
            num_results=10000,
            num_burnin_steps=5000,
            current_state=[
                tf.ones([], name='init_switchpoint'),
                tf.ones([], name='init_pre_switch_average'),
                tf.ones([], name='init_post_switch_average'),
            ],
            trace_fn=None,
            kernel=kernel,
        )

        return states


    @classmethod
    def sample(cls, count_data):
        target_log_prob_fn = lambda s, m1, m2: cls.target_log_prob_fn(s, m1, m2, count_data)
        timeperiod_length = len(count_data)

        return [
            s.numpy()
            for s in cls.make_chain(
                target_log_prob_fn=target_log_prob_fn,
                timeperiod_length=timeperiod_length,
            )
        ]
