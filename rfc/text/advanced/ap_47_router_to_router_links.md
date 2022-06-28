# Router-to-Router Links {#r2r-links}

Write me.

1. Resolve global realm name R_name via ENS to the on-chain address R_adr of the realm.
2. Retrieve list of Domains R_DR routing realm R_adr.
3. Retrieve the node's N1 own domain D_N1 given the node's address N1_adr.
4. Check D_N1 is in R_DR.
5. Select a domain D (!=D_N1) from R_DR and get endpoint E for D.
6. Connect to D and authenticate via WAMP-Cryptosign.
7. Verify connected node N2 by checking against D
8. Subscribe to `wamp.r2r.traffic_payable`
9. When receiving a traffic payable event, buy the respective key by
calling `xbr.pool.buy_key`, and calling `wamp.r2r.submit_traffic_payment`, which returns a traffic usage report.

Data Spaces are end-to-end encrypted routing realms connecting data driven microservices.

The message routing between the microservice endpoints in
