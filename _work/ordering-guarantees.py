# this is using Z3 solver
#
#   https://www.microsoft.com/en-us/research/project/z3-3/
#   https://github.com/Z3Prover/z3
#
# for python
#
#   pip install z3-solver

# Message Conversation Log (MCL)
#
# The message conversation log records all WAMP messages on
# all WAMP sessions connected to a router:
#
# set[(sess_name, msg_glc, msg_dir, msg_type, ...)]
#
# * sess_name: symbolic session name
# * msg_glc: message send/receive global logical clock
# * msg_dir: message direction
# * msg_type: WAMP message type
# * ...: rest of WAMP message
#
MCL = set([

    # HELLO
    # https://wamp-proto.org/wamp_latest_ietf.html#section-4.1.1-26
    ['S1', 1, 'TX', 1, "realm1", {
        "agent": "wamp-verifier-client",
        "roles": {
            "subscriber": {},
            "publisher": {},
            "caller": {},
            "callee": {},
        }
    }],

    # WELCOME
    # https://wamp-proto.org/wamp_latest_ietf.html#section-4.1.1-28
    ['S1', 2, 'RX', 2, 9129137332, {
        "agent": "wamp-verifier-router",
        "roles": {
            "broker": {},
            "dealer": {}
        }
    }],

    # REGISTER
    # https://wamp-proto.org/wamp_latest_ietf.html#section-6.1.1-5
    ['S1', 3, 'TX', 64, 25349185, {}, "com.myapp.echo"],

    # REGISTERED
    # https://wamp-proto.org/wamp_latest_ietf.html#section-6.1.2-5
    ['S1', 4, 'RX', 65, 25349185, 2103333224],

    # CALL
    # https://wamp-proto.org/wamp_latest_ietf.html#section-6.2.1-11
    ['S1', 5, 'TX', 48, 7814135, {}, "com.myapp.echo", ["Hello, world!"]],

    # INVOCATION
    # https://wamp-proto.org/wamp_latest_ietf.html#section-6.2.2-11
    ['S1', 6, 'RX', 68, 6131533, 2103333224, {}, ["Hello, world!"]],

    # YIELD
    # https://wamp-proto.org/wamp_latest_ietf.html#section-6.2.3-11
    ['S1', 7, 'TX', 70, 6131533, {}, ["Hello, world!"]],

    # RESULT
    # https://wamp-proto.org/wamp_latest_ietf.html#section-6.2.4-11
    ['S1', 8, 'RX', 50, 7814135, {}, ["Hello, world!"]],

    # GOODBYE
    # https://wamp-proto.org/wamp_latest_ietf.html#section-4.2.1-11
    ['S1', 9, 'TX', 6, {}, "wamp.close.close_realm"],

    # GOODBYE
    # https://wamp-proto.org/wamp_latest_ietf.html#section-4.2.1-13
    ['S1', 10, 'RX', 6, {}, "wamp.close.goodbye_and_out"],
])
