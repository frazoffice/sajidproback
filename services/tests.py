import stripe

SECRET_KEY = "sk_test_51KgS9FE4k21uIFp3L7zSMYNk6viikCXl4MzIJgBceMXbxay08a34Q0kI5YzxWieTiIEtrVmcYElEEYnVSRIDmhRS00AFRm8VaP"

stripe.api_key=SECRET_KEY

def generate_card_token(cardnumber,expmonth,expyear,cvv):
    data= stripe.Token.create(
            card={
                "number": str(cardnumber),
                "exp_month": int(expmonth),
                "exp_year": int(expyear),
                "cvc": str(cvv),
            })
    card_token = data['id']

    return card_token

token=generate_card_token("4242 4242 4242 4242","12","34","567")

def create_payment_charge(tokenid,amount):

    payment = stripe.Charge.create(
        amount= int(amount)*100,                  # convert amount to cents
        currency='usd',
        description='Example charge',
        source=tokenid,
    )

    payment_check = payment['paid']    # return True for successfull payment

    return payment_check
data=create_payment_charge(token,1000)
print(data)
