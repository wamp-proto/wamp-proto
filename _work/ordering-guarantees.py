# this is using Z3 solver
#
#   https://www.microsoft.com/en-us/research/project/z3-3/
#   https://github.com/Z3Prover/z3
#
# for python
#
#   pip install z3-solver

from z3 import *
from autobahn.wamp.message import Hello, Abort, Goodbye, Welcome, Call, Invocation, Yield, Result, Register, Registered
from autobahn.wamp.serializer import Serializer

RX = 1
TX = 2

TR1 = 1
TR2 = 2

# Message Conversation Log (MCL)
#
# The message conversation log records all WAMP messages on
# all WAMP sessions connected to a router:
#
# MCL: Dict(msg_glc, (msg_trnp, msg_dir, msg_type, <rest of WAMP message>)
#
# * msg_trnp: message transport
# * msg_glc: message send/receive global logical clock
# * msg_dir: message direction
# * msg_type: WAMP message type
#
MCL_VALID = {

    # HELLO
    # https://wamp-proto.org/wamp_latest_ietf.html#section-4.1.1-26
    1: (TR1, TX, Hello.MESSAGE_TYPE, "realm1", {
        "agent": "wamp-verifier-client1",
        "roles": {
            "subscriber": {},
            "publisher": {},
            "caller": {},
            "callee": {},
        }
    }),

    # HELLO
    # https://wamp-proto.org/wamp_latest_ietf.html#section-4.1.1-26
    2: (TR2, TX, Hello.MESSAGE_TYPE, "realm1", {
        "agent": "wamp-verifier-client2",
        "roles": {
            "subscriber": {},
            "publisher": {},
            "caller": {},
            "callee": {},
        }
    }),

    # WELCOME
    # https://wamp-proto.org/wamp_latest_ietf.html#section-4.1.1-28
    3: (TR1, RX, Welcome.MESSAGE_TYPE, 9129137332, {
        "agent": "wamp-verifier-router1",
        "roles": {
            "broker": {},
            "dealer": {}
        }
    }),

    # WELCOME
    # https://wamp-proto.org/wamp_latest_ietf.html#section-4.1.1-28
    4: (TR2, RX, Welcome.MESSAGE_TYPE, 5592343255, {
        "agent": "wamp-verifier-router1",
        "roles": {
            "broker": {},
            "dealer": {}
        }
    }),

    # REGISTER
    # https://wamp-proto.org/wamp_latest_ietf.html#section-6.1.1-5
    5: (TR1, TX, Register.MESSAGE_TYPE, 25349185, {}, "com.myapp.echo"),

    # REGISTERED
    # https://wamp-proto.org/wamp_latest_ietf.html#section-6.1.2-5
    6: (TR1, RX, Registered.MESSAGE_TYPE, 25349185, 2103333224),

    # CALL
    # https://wamp-proto.org/wamp_latest_ietf.html#section-6.2.1-11
    7: (TR2, TX, Call.MESSAGE_TYPE, 7814135, {}, "com.myapp.echo", ["Hello, world!"]),

    # INVOCATION
    # https://wamp-proto.org/wamp_latest_ietf.html#section-6.2.2-11
    8: (TR1, RX, Invocation.MESSAGE_TYPE, 6131533, 2103333224, {}, ["Hello, world!"]),

    # YIELD
    # https://wamp-proto.org/wamp_latest_ietf.html#section-6.2.3-11
    9: (TR1, TX, Yield.MESSAGE_TYPE, 6131533, {}, ["Hello, world!"]),

    # RESULT
    # https://wamp-proto.org/wamp_latest_ietf.html#section-6.2.4-11
    10: (TR2, RX, Result.MESSAGE_TYPE, 7814135, {}, ["Hello, world!"]),

    # GOODBYE
    # https://wamp-proto.org/wamp_latest_ietf.html#section-4.2.1-11
    11: (TR1, TX, Goodbye.MESSAGE_TYPE, {}, "wamp.close.close_realm"),

    # GOODBYE
    # https://wamp-proto.org/wamp_latest_ietf.html#section-4.2.1-13
    12: (TR2, RX, Goodbye.MESSAGE_TYPE, {}, "wamp.close.goodbye_and_out"),
}


# invalid: the first message on any transport must be HELLO sent by the client
MCL_INVALID1 = {
    # REGISTER
    # https://wamp-proto.org/wamp_latest_ietf.html#section-6.1.1-5
    1: (TR1, TX, Register.MESSAGE_TYPE, 25349185, {}, "com.myapp.echo"),
}


# invalid: the first message on any transport must be HELLO sent (!) by the client
MCL_INVALID2 = {
    # HELLO
    # https://wamp-proto.org/wamp_latest_ietf.html#section-4.1.1-26
    1: (TR1, RX, Hello.MESSAGE_TYPE, "realm1", {
        "agent": "wamp-verifier-router1",
        "roles": {
            "broker": {},
            "dealer": {}
        }
    }),
}


# invalid: the WELCOME must be received after sending HELLO
MCL_INVALID3 = {

    # WELCOME
    # https://wamp-proto.org/wamp_latest_ietf.html#section-4.1.1-28
    1: (TR1, RX, Welcome.MESSAGE_TYPE, 9129137332, {
        "agent": "wamp-verifier-router1",
        "roles": {
            "broker": {},
            "dealer": {}
        }
    }),

    # HELLO
    # https://wamp-proto.org/wamp_latest_ietf.html#section-4.1.1-26
    2: (TR1, TX, Hello.MESSAGE_TYPE, "realm1", {
        "agent": "wamp-verifier-client1",
        "roles": {
            "subscriber": {},
            "publisher": {},
            "caller": {},
            "callee": {},
        }
    }),
}

MCLS = [MCL_VALID, MCL_INVALID1, MCL_INVALID2, MCL_INVALID3]

s = Solver()

# the first WAMP message on any peer connection must be HELLO sent by the peer
first_msg_dir, first_msg_type = Int(MCL_VALID[1][1]), Int(MCL_VALID[1][2])
s.add(first_msg_dir == TX, first_msg_type == Hello.MESSAGE_TYPE)

# to do: check for other WAMP protocol rules

for k in sorted(MCL_VALID.keys()):
    evt = MCL_VALID[k]
    sess_name, msg_dir, msg_type = evt[0:3]
    if msg_type == Hello.MESSAGE_TYPE:
        print("Hello")
    elif msg_type == Welcome.MESSAGE_TYPE:
        print("Welcome")
    else:
        print("Other")
