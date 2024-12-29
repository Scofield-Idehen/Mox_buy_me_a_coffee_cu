from interfaces import AggregatorV3Interface

magicNumber: constant(uint256) = 1 * (10 ** 18)

@internal
@view
def ETH_USD(price_feed: AggregatorV3Interface, eth_amount: uint256) -> uint256:#takes a paremeneter for the price 
    price: int256 = staticcall price_feed.latestAnswer() # checks the current ETh price
    eth_price: uint256 = convert(price, uint256) * (10 ** 10) #convert to uint as it is in int
    eth_amount_in_USD: uint256 = (eth_amount * eth_price) // magicNumber #reomve the extra decimal places 

    return eth_amount_in_USD