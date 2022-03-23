import stripe

from project_backend.settings import SECRET_KEY
stripe.api_key=SECRET_KEY
def generate_card_token(cardnumber,expmonth,expyear,cvv):
    try:
        data= stripe.Token.create(
                card={
                    "number": str(cardnumber),
                    "exp_month": int(expmonth),
                    "exp_year": int(expyear),
                    "cvc": str(cvv),
                })
        card_token = data['id']
    except:
        card_token=False
    return card_token



def create_payment_charge(tokenid,amount):

    payment = stripe.Charge.create(
        amount= int(amount)*100,                  # convert amount to cents
        currency='usd',
        description='Example charge',
        source=tokenid,
    )

    payment_check = payment['paid']    # return True for successfull payment

    return payment_check
# data=create_payment_charge(token,1000)
# print(data)
