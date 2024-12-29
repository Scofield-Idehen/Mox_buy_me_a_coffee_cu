# pragma version ^ 0.4.0

"""
@ license MIT
@ title Buy me a coffee
@ author: Scofield Idehen
@ notice: this contract is about building a contract 
"""

from interfaces import AggregatorV3Interface
import getPrice


#storage veriable 

#mim_USD: public(constant(uint256)) = as_wei_value(5, "ether") #constant are not storage vairable 
min_USD: public(constant(uint256)) = as_wei_value(5, "ether") #constant are not storage vairable
priceFeed: public(immutable(AggregatorV3Interface))
owner: public(immutable(address))
funders: public(DynArray[address, 1000])

#map address to amount in uint256
funder_to_funders: public(HashMap[address, uint256])

@deploy
def __init__(price_feed: address): #we can pass the address we want sapolia or any other 
    priceFeed = AggregatorV3Interface(price_feed) #here we pass Sapolia 
    owner = msg.sender

@external
@payable 
def fund():
    self._fund() 

@internal
@payable
def _fund():
    usd_value_of_eth: uint256 = getPrice.ETH_USD(priceFeed, msg.value)
    assert usd_value_of_eth >= min_USD  #1000000000000000000 #why dont we pass the min to init?
    self.funders.append(msg.sender)
    self.funder_to_funders[msg.sender] += msg.value

@external 
def withdraw():
    assert msg.sender == owner, "not contract owner "
    #send(self.owner, self.balance)
    raw_call(owner, b"", value= self.balance)
    self.funders = [] #reset the array to zero
    for funder: address in self.funders:
        self.funder_to_funders[funder] = 0
    self.funders = []



@external 
@view
def get_eth_to_usd_rate(eth_amount: uint256) -> uint256:
    return getPrice.ETH_USD(priceFeed, eth_amount)

@external
@view
def get_price(eth_amount: uint256) -> uint256:
    return getPrice.ETH_USD(priceFeed, eth_amount)




@external 
@payable
def __default__():
    self._fund() 