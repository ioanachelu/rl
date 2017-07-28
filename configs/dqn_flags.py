import tensorflow as tf
from configs import base_flags

# Basic model parameters.
tf.app.flags.DEFINE_string('game', 'Catcher-v0',
                           """Experiment name from Atari platform""")
tf.app.flags.DEFINE_boolean('monitor', False,
                            """Wrap env in monitor""")
tf.app.flags.DEFINE_boolean('layer_norm', False,
                            """Use layer normalization""")
tf.app.flags.DEFINE_boolean('show_training', True,
                            """Show windows with workers training""")
tf.app.flags.DEFINE_integer('summary_interval', 500, """Number of episodes of interval between summary saves""")
tf.app.flags.DEFINE_integer('checkpoint_interval', 500, """Number of episodes of interval between checkpoint saves""")
tf.app.flags.DEFINE_integer('agent_history_length', 1, """Number of frames that makes every state""")
tf.app.flags.DEFINE_integer('resized_width', 24, """Resized width of each frame""")
tf.app.flags.DEFINE_integer('resized_height', 24, """Resized height of each frame""")
tf.app.flags.DEFINE_float('gamma', 0.99, """Gamma value""")
tf.app.flags.DEFINE_float('lr', 0.000635, """Learning rate""")
tf.app.flags.DEFINE_string('optimizer', "Adam", """optimizer""")
tf.app.flags.DEFINE_integer('seed', 23, """seed value for the gym env""")
tf.app.flags.DEFINE_integer('hidden_size', 128, """hidden_size of FC layer""")
tf.app.flags.DEFINE_integer('batch_size', 96, """batch_size""")
tf.app.flags.DEFINE_integer('update_freq', 4, """update_freq""")
tf.app.flags.DEFINE_integer('target_update_freq', 24, """target_update_freq""")
tf.app.flags.DEFINE_integer('gradient_norm_clipping', 10, """gradient_norm_clipping""")
tf.app.flags.DEFINE_integer('memory_size', 100000, """memory_size""")
tf.app.flags.DEFINE_integer('explore_steps', 100000, """explore_steps""")
tf.app.flags.DEFINE_integer('observation_steps', 12500, """observation_steps""")
tf.app.flags.DEFINE_integer('max_total_steps', 1200000, """max_total_steps""")
tf.app.flags.DEFINE_float('initial_random_action_prob', 1.0, """initial_random_action_prob""")
tf.app.flags.DEFINE_float('final_random_action_prob', 0.05, """initial_random_action_prob""")




