The following state chart gives the states that a WAMP peer can be in during the session lifetime cycle.

{align="left"}
                             +--------------+                           
    +--------(6)------------->              |                           
    |                        | CLOSED       <--------------------------+
    | +------(4)------------->              <---+                      |
    | |                      +--------------+   |                      |
    | |                               |         |                      |
    | |                              (1)       (7)                     |
    | |                               |         |                      |
    | |                      +--------v-----+   |                   (11)
    | |                      |              +---+                      |
    | |         +------------+ ESTABLISHING +----------------+         |
    | |         |            |              |                |         |
    | |         |            +--------------+                |         |
    | |         |                     |                     (10)       |
    | |         |                    (9)                     |         |
    | |         |                     |                      |         |
    | |        (2)           +--------v-----+       +--------v-------+ |
    | |         |            |              |       |                | |
    | |         |     +------> FAILED       <--(13)-+ CHALLENGING /  +-+
    | |         |     |      |              |       | AUTHENTICATING |  
    | |         |     |      +--------------+       +----------------+  
    | |         |    (8)                                     |          
    | |         |     |                                      |          
    | |         |     |                                      |          
    | | +-------v-------+                                    |          
    | | |               <-------------------(12)-------------+          
    | | | ESTABLISHED   |                                               
    | | |               +--------------+                                
    | | +---------------+              |                                
    | |         |                      |                                
    | |        (3)                    (5)                               
    | |         |                      |                                
    | | +-------v-------+     +--------v-----+                          
    | | |               +--+  |              |                          
    | +-+ SHUTTING DOWN |  |  | CLOSING      |                          
    |   |               |(14) |              |                          
    |   +-------^-------+  |  +--------------+                          
    |           |----------+           |                                
    +----------------------------------+     


| #  |  State |
|----|--------|
| 1  | Sent HELLO   |
| 2  | Received WELCOME  |
| 3  | Sent GOODBYE  |
| 4  | Received GOODBYE  |
| 5  | Received GOODBYE  |
| 6  | Sent GOODBYE  |
| 7  | Received invalid HELLO / Send ABORT  |
| 8  | Received HELLO or AUTHENTICATE  |
| 9  | Received other  |
| 10 | Received valid HELLO [needs authentication] / Send CHALLENGE  |
| 11 | Received invalid AUTHENTICATE / Send ABORT  |
| 12 | Received valid AUTHENTICATE / Send WELCOME  |
| 13 | Received other  |
| 14 | Received other / ignore  |


