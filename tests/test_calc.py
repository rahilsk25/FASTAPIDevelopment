from app.calculations import add_number, sub_number, BankAccount
import pytest


@pytest.fixture
def zero_bankaccount():
    print('Creating zero balance bank account')
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)
# @pytest.mark.parametrize("x, y, result", [
#     (5,8,13),
#     (60,80,140),
#     (1,1,2)
# ])
# def test_add(x,y,result):
#     assert add_number(x,y)==result


# @pytest.mark.parametrize("x, y, result", [
#     (5,8,-3),
#     (80,60,20),
#     (1,1,0)
# ])
# def test_subtract(x,y, result):
#     assert sub_number(x,y)==result

def test_bank_Set_initial_amount(zero_bankaccount):
    print("testing my bank account balance")
    assert zero_bankaccount.balance==0


def test_bank(bank_account):
    print("testing my bank account balance")
    with pytest.raises(Exception):
        bank_account.withdraw(70)
    