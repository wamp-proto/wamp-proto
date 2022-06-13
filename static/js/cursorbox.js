(function() {

   "use strict";

   var url = 'wss://demo.crossbar.io/ws';
   var realm = 'crossbardemo';

   var session = null;

   var _idchars = "0123456789";
   var _idlen = 6;
   var _idpat = /^\d*$/;


   function updateStatusline(status, node) {
      // console.log('demo_howfast:', status, node);

      document.getElementById("statusline").innerHTML = status;
      if(node) {
         document.querySelector(".connectorInstance > p").innerHTML = node;
      } else {
         document.querySelector(".connectorInstance > p").innerHTML = "";
      }
   };

   function now() {
      if ('performance' in window && 'now' in performance) {
         return performance.now();
      } else {
         return (new Date).getTime();
      }
   }

   function randomChannelId() {
      var id = "";
      for (var i = 0; i < _idlen; i += 1) {
         id += _idchars.charAt(Math.floor(Math.random() * _idchars.length));
      }
      return id;
   };

   var _cnt_sent = 0;
   var _cnt_received = 0;

   var connection = null;

   function connect() {

      connection = new autobahn.Connection({
         url: url,
         realm: realm,
         max_retries: 30,
         initial_retry_delay: 2
         }
      );

      connection.onopen = function (sess, details) {

         console.log("onopen realtime box", arguments);

         var node = "";
         switch(details.x_cb_node_id) {
            case("cbdemo-eu-central-1"):
               node = "Frankfurt/Main, Germany";
               break;
            case("cbdemo-us-west-1"):
               node = "Northern California";
               break;
            default:
               // do nothing;
         }
         console.log("node", node);

         if (details.x_cb_node_id) {
            updateStatusline("Connected to node <strong>" + details.x_cb_node_id + "</strong> at URL <strong>" + url + "</strong>", node);
         } else {
            updateStatusline("Connected to URL <strong>" + url + "</strong>", node);
         }

         session = sess;
         setupDemo();
      };

      connection.onclose = function (reason, details) {
         session = null;
         console.log("connection closed ", reason, details);

          if (details.will_retry) {
            updateStatusline("Trying to reconnect in " + parseInt(details.retry_delay) + " s.", "");
         } else {
            updateStatusline("Disconnected", "");
         }
      }

      connection.open();

   }

   function setupDemo() {

      _cnt_sent = 0;
      _cnt_received = 0;

      function setCursorPosition (box, offsetX, offsetY) {
         // we adjust the position of a cursor representation,
            // offset a bit from the actual position - implement me!
            // check that this does maxes out at the vertical + horizontal dimensions of the box (- the dimensions of the cursor)

         // //  right and left border
         // if (offsetX > elements[box].offsetWidth - 20) {
         //    offsetX = elements[box].offsetWidth - 20;
         // }
         //
         // // top and bottom border
         // if (offsetY > elements[box].offsetHeight - 21) {
         //    offsetY = elements[box].offsetHeight - 21;
         // }

         //  right and left border
         if (offsetX > elements[box].offsetWidth - 64) {
            offsetX = elements[box].offsetWidth - 64;
         }

         // top and bottom border
         if (offsetY > elements[box].offsetHeight - 55) {
            offsetY = elements[box].offsetHeight - 55;
         }

         if (offsetY < -2 ) {
            offsetY = -2;
         }

         if (offsetX < -0 ) {
            offsetX = -0;
         }

         elements[box + "cursor"].style.left = (offsetX) + "px";
         elements[box + "cursor"].style.top = (offsetY) + "px";
      }

      function onMouseMove (evt) {

         // console.log("onMouseMove", evt);
         // console.log(typeof(evt));

         if (!session) {
            // don't move if not connected
            return;
         }

         // we get the box this occurs on
         var box = evt.target.id;

         // exclude events on the border of the box
         if (box != "box1" && box != "box2" ) {
            return;
         }

         var offsetX = null;
         var offsetY = null;

         if(evt.type === "mousemove") {

            // we get the current position within the box (offset)
            // offsetX = evt.offsetX + 3;
            // offsetY = evt.offsetY - 12;
            offsetX = evt.offsetX;
            offsetY = evt.offsetY;

         } else if (evt.type === "touchmove") {

            evt.preventDefault();

            // we get the position within the screen
            // (have not found any property that would be relative to the box)
            var offsetPageX = evt.changedTouches[0].pageX;
            var offsetPageY = evt.changedTouches[0].pageY;

            var offsetBoxX = elements[box].offsetLeft;
            var offsetBoxY = elements[box].offsetTop;

            offsetX = offsetPageX - offsetBoxX;
            offsetY = offsetPageY - offsetBoxY;

         } else {
            throw new Error("unknown event type");
         }


         setCursorPosition(box, offsetX, offsetY);

         // we publish this position
         session.publish(
            "io.crossbar.demo.cursor_sync." + channel,
            null,
            {
               box: box,
               offsetX: offsetX,
               offsetY: offsetY,
               sent: now()
            },
            {
               exclude_me: false
            }
         );
         _cnt_sent += 1;
      };

      // we generate the channel ID
      var channel = randomChannelId();
      // we get the two elements
      var elements = {};

      elements.box1 = document.getElementById("box1");
      elements.box2 = document.getElementById("box2");
      elements.box1cursor = document.getElementById("box1cursor");
      elements.box2cursor = document.getElementById("box2cursor");

      // we attach our event listeners
      elements.box1.addEventListener("mousemove", onMouseMove);
      elements.box2.addEventListener("mousemove", onMouseMove);
      elements.box1.addEventListener("touchmove", onMouseMove);
      elements.box2.addEventListener("touchmove", onMouseMove);

      var onReceiveMouseMove = function (args, kwargs) {

         _cnt_received += 1;

         var rtt = (Math.round(10 * (now() - kwargs.sent)) / 10.).toFixed(1);
         updateStatusline("<strong>" + rtt + " ms</strong> last event round-trip time (" + _cnt_sent + "/" + _cnt_received + " events sent/received)");

         var box = kwargs.box === "box1" ? "box2" : "box1";

         setCursorPosition(box, kwargs.offsetX, kwargs.offsetY);
      }

      session.subscribe("io.crossbar.demo.cursor_sync." + channel, onReceiveMouseMove);
   }

   connect();

})()
