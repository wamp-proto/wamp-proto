### Event Retention

#### Feature Definition

Event Retention is where a particular topic has an event associated with it which is delivered upon an opting-in client subscribing to the topic.

It can be used for topics that generally have single or very few Publishers notifying Subscribers of a single updating piece of data -- for example, a topic where a sensor publishes changes of temperature & humidity in a data center.
It may do this every time the data changes (making the time between updates potentially very far apart), which causes an issue fornew Subscribers who may need the last-known value upon connection, rather than waiting an unknown period of time until it is updated.
Event Retention covers this use case by allowing the Publisher to mark a event as 'retained', bound to the topic it was sent to, which can be delivered upon a new client subscription that asks for it.
It is similar to Event History, but allows the publisher to decide what the most important recent event is on the topic, even if other events are being delivered.

A *Broker* that advertises support MAY provide *event retention* on topics it provides.
This event retention SHOULD be provided on a best-effort basis, and MUST NOT be interpreted as permanent or reliable storage by clients.
This event retention is limited to one event that all subscribers would recieve, and MAY include other supplemental events that have limited distribution (for example, a event published with subscriber black/whitelisting).

A *Publisher* can request storage of a new Retained Event by setting `Publish.Options.retain|bool` to `true`.
Lack of the key in `Publish.Options` MUST be interpreted as a `false` value.
A Broker MAY decline to provide event retention on certain topics by ignoring the `Publish.Options.retain` value.
Brokers that allow event retention on the given topic MUST set the topic Retained Event to this if it were eligible to be published on the topic.

*Subscribers* may request access to the Retained Event by setting `Subscribe.Options.get_retained|bool` to `true`.
Lack of the key in `Subscribe.Options` MUST be interpreted as a `false` value.
When they opt-in to receiving the Retained Event, the Broker MUST send the Subscriber the **most recent** Retained Event that they would have received if they were subscribing when it was published.
The Broker MUST NOT send the Subscriber a Retained Event that they would not be eligible to receive if they were subscribing when it was published.
The *Retained Event*, as sent to the subscribing client, MUST have `Event.Details.retained|bool` set to `true`, to inform subscribers that it is not an immediately new message.

#### Feature Announcement

Support for this feature MUST be announced by *Brokers* (`role := "broker"`) via

{align="left"}
        Welcome.Details.roles.broker.features.event_retention|bool := true
