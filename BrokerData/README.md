# Get All Broker Data

Brokers Name

```
brokers_name = [x.text for x in self.broswer.find_elements_by_xpath("//select[@name='sel_Broker']/option")]
```

Broker ID

```
brokers_id = [x.get_attribute('value') for x in self.broswer.find_elements_by_xpath("//select[@name='sel_Broker']/option")]
```

You can search the stock from the broker_branch string

example:

```
db.getCollection('stock').find({"data":{"$elemMatch" : { "brokerbranch": "6160_6168"}}})
```
