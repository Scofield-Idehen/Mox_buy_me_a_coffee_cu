from eth_utils import to_wei
from moccasin.config import get_active_network
import boa

SEND_VALUE = to_wei(1, "ether")
NEW_OWNERS = []
RANDOM_OWNER  = boa.env.generate_address("Not_owner")
accounts = [boa.env.generate_address(f"account{i}") for i in range(10)]



for i in range(11):
    new_address = boa.env.generate_address(f"Not_owner{i}")
    NEW_OWNERS.append(new_address)

def test_price_is_correct(coffee, eth_coffee):
    assert coffee.priceFeed() == eth_coffee.address

def test_owner_is_correct(coffee, deployer):
    assert coffee.min_USD() == to_wei(5, "ether")
    assert coffee.owner() == deployer.address

def test_fund_updates_funders(coffee, deployer):
    
    # Arrange
    boa.env.set_balance(accounts[0], to_wei(2, "ether"))
    boa.env.set_balance(deployer.address, to_wei(2, "ether"))
    account = deployer
 
   
    # Act
    coffee.fund(sender=account.address, value=to_wei(1, "ether"))
    # Assert
    assert coffee.funders(0) == account.address

def test_default_fallback_function(coffee):
    with boa.reverts():
        coffee.fund()


def test_with_moneys(coffee, deployer):
    boa.env.set_balance(deployer.address, SEND_VALUE)
    #act
    coffee.fund(value=SEND_VALUE)
    #assert
    funder = coffee.funders(0)
    assert funder == deployer.address
    assert coffee.funder_to_funders(funder) == SEND_VALUE

def test_Onwer_cannot_withdraw(coffee, deployer):
    boa.env.set_balance(deployer.address, SEND_VALUE) #set address and give eth value 
    #act
    coffee.fund(value=SEND_VALUE)

    with boa.env.prank(RANDOM_OWNER):
        with boa.reverts():
            coffee.withdraw()

def test_owner_can_withdraw(coffee, deployer):
    boa.env.set_balance(coffee.owner(), SEND_VALUE)
    with boa.env.prank(coffee.owner()):
        coffee.fund(value= SEND_VALUE)
        coffee.withdraw()
    assert boa.env.get_balance(coffee.address) == 0


def test_multiple_funders_and_withdrawal(coffee, deployer):
    # Setup 10 funders with funds
    for address in NEW_OWNERS[:10]:  # Use first 10 addresses
        boa.env.set_balance(address, SEND_VALUE)
        with boa.env.prank(address):
            coffee.fund(value=SEND_VALUE)
    
    # Verify all funders contributed
    for i in range(10):
        assert coffee.funders(i) == NEW_OWNERS[i]
        assert coffee.funder_to_funders(NEW_OWNERS[i]) == SEND_VALUE
    
    # Verify total contract balance
    expected_balance = SEND_VALUE * 10
    assert boa.env.get_balance(coffee.address) == expected_balance
    
    # Withdraw as owner
    owner_initial_balance = boa.env.get_balance(coffee.owner())
    with boa.env.prank(coffee.owner()):
        coffee.withdraw()
    
    # Verify withdrawal
    assert boa.env.get_balance(coffee.address) == 0  # Contract should be empty
    # Verify owner received the funds (should be initial balance + all funds)
    assert boa.env.get_balance(coffee.owner()) == owner_initial_balance + expected_balance


def test_get_eth_to_usd_rate(coffee):
    assert coffee.get_price(SEND_VALUE) > 0
    