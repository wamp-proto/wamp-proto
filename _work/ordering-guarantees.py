# this is using Z3 solver
#
#   https://www.microsoft.com/en-us/research/project/z3-3/
#   https://github.com/Z3Prover/z3
#
# for python
#
#   pip install z3-solver

from z3 import *

# Message Conversation Log (MCL)
#
# The message conversation log records all WAMP messages on
# all WAMP sessions connected to a router:
#
# MCL: Dict(msg_glc, (sess_name, msg_dir, msg_type, ...)
#
# * sess_name: symbolic session name
# * msg_glc: message send/receive global logical clock
# * msg_dir: message direction
# * msg_type: WAMP message type
# * ...: rest of WAMP message
#
MCL = {

    # HELLO
    # https://wamp-proto.org/wamp_latest_ietf.html#section-4.1.1-26
    1: ('S1', 'TX', 1, "realm1", {
        "agent": "wamp-verifier-client",
        "roles": {
            "subscriber": {},
            "publisher": {},
            "caller": {},
            "callee": {},
        }
    }),

    # WELCOME
    # https://wamp-proto.org/wamp_latest_ietf.html#section-4.1.1-28
    2: ('S1', 'RX', 2, 9129137332, {
        "agent": "wamp-verifier-router",
        "roles": {
            "broker": {},
            "dealer": {}
        }
    }),

    # REGISTER
    # https://wamp-proto.org/wamp_latest_ietf.html#section-6.1.1-5
    3: ('S1', 'TX', 64, 25349185, {}, "com.myapp.echo"),

    # REGISTERED
    # https://wamp-proto.org/wamp_latest_ietf.html#section-6.1.2-5
    4: ('S1', 'RX', 65, 25349185, 2103333224),

    # CALL
    # https://wamp-proto.org/wamp_latest_ietf.html#section-6.2.1-11
    5: ('S1', 'TX', 48, 7814135, {}, "com.myapp.echo", ["Hello, world!"]),

    # INVOCATION
    # https://wamp-proto.org/wamp_latest_ietf.html#section-6.2.2-11
    6: ['S1', 'RX', 68, 6131533, 2103333224, {}, ["Hello, world!"]],

    # YIELD
    # https://wamp-proto.org/wamp_latest_ietf.html#section-6.2.3-11
    7: ['S1', 'TX', 70, 6131533, {}, ["Hello, world!"]],

    # RESULT
    # https://wamp-proto.org/wamp_latest_ietf.html#section-6.2.4-11
    8: ('S1', 'RX', 50, 7814135, {}, ["Hello, world!"]),

    # GOODBYE
    # https://wamp-proto.org/wamp_latest_ietf.html#section-4.2.1-11
    9: ('S1', 'TX', 6, {}, "wamp.close.close_realm"),

    # GOODBYE
    # https://wamp-proto.org/wamp_latest_ietf.html#section-4.2.1-13
    10: ('S1', 'RX', 6, {}, "wamp.close.goodbye_and_out"),
}

