// This is your test publishable API key.
const stripe = Stripe(STRIPE_PK);

// The items the customer wants to buy
const items = [JSON.parse(localStorage.getItem('cart'))];

let elements;

// Fetches a payment intent and captures the client secret
async function initialize() {
  const response = await fetch(PAYMENT_INTENT_ROUTE, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ items }),
  });
  const { clientSecret } = await response.json();

  const appearance = {
    theme: 'night',
    variables : {
        colorPrimary: '#0092ca'
    },
    rules: {
        'Input': {
            fontFamily: 'Quicksand, sans-serif',
            colorText: '#eeeeee',
            colorTextPlaceholder: '#eeeeee'
        },
        '.Input:focus': {
            boxShadow: '0px 1px 1px rgba(0, 0, 0, 0.03), 0px 3px 6px rgba(18, 42, 66, 0.02), 0 0 0px 1px #0092ca'
        }
    }
  };
  elements = stripe.elements({ appearance, clientSecret });


  const paymentElementOptions = {
    layout: "tabs",
  };

  const paymentElement = elements.create("payment", paymentElementOptions);
  paymentElement.mount("#payment-element");

  // Create and mount the Address Element in shipping mode
  const addressElement = elements.create("address", {
    mode: "shipping",
    autocomplete: {
        mode: "google_maps_api",
        apiKey: GOOGLE_MAPS_KEY,
    },
  });
  addressElement.mount("#address-element");
  addressElement.on('change', (event) => {
      if (event.complete){
        // Extract potentially complete address
        const address = event.value.address;
      }
    })
}

async function handleSubmit(e) {
  e.preventDefault();
  setLoading(true);

  const { error } = await stripe.confirmPayment({
    elements,
    confirmParams: {
      // Make sure to change this to your payment completion page
      return_url: SUCCESSFUL_PAYMENT,
      receipt_email: document.getElementById("email").value,
    },
  });

  // This point will only be reached if there is an immediate error when
  // confirming the payment. Otherwise, your customer will be redirected to
  // your `return_url`. For some payment methods like iDEAL, your customer will
  // be redirected to an intermediate site first to authorize the payment, then
  // redirected to the `return_url`.
  if (error.type === "card_error" || error.type === "validation_error") {
    showMessage(error.message);
  } else {
    showMessage("An unexpected error occurred.");
  }

  setLoading(false);
}

// Fetches the payment intent status after payment submission
async function checkStatus() {
  const clientSecret = new URLSearchParams(window.location.search).get(
    "payment_intent_client_secret"
  );

  if (!clientSecret) {
    return;
  }

  const { paymentIntent } = await stripe.retrievePaymentIntent(clientSecret);

  switch (paymentIntent.status) {
    case "succeeded":
      showMessage("Payment succeeded!");
      break;
    case "processing":
      showMessage("Your payment is processing.");
      break;
    case "requires_payment_method":
      showMessage("Your payment was not successful, please try again.");
      break;
    default:
      showMessage("Something went wrong.");
      break;
  }
}

// Show Order total

const showOrderTotal = () => {
    document.getElementById('total').innerText = JSON.parse(localStorage.getItem('cart'))['total'].toLocaleString("en-US", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });
}

// ------- UI helpers -------

function showMessage(messageText) {
  const messageContainer = document.querySelector("#payment-message");

  messageContainer.classList.remove("hidden");
  messageContainer.textContent = messageText;

  setTimeout(function () {
    messageContainer.classList.add("hidden");
    messageContainer.textContent = "";
  }, 4000);
}

 //Show a spinner on payment submission
function setLoading(isLoading) {
  if (isLoading) {
    // Disable the button and show a spinner
    document.querySelector("#submit").disabled = true;
    document.querySelector("#spinner").classList.remove("hidden");
    document.querySelector("#button-text").classList.add("hidden");
  } else {
    document.querySelector("#submit").disabled = false;
    document.querySelector("#spinner").classList.add("hidden");
    document.querySelector("#button-text").classList.remove("hidden");
  }
}

if (Object.keys(JSON.parse(localStorage.getItem('cart'))).length > 3){
    initialize();
    document.getElementById('submit').disabled = false
    checkStatus();
} else {
    document.getElementById('submit').disabled = true
}
showOrderTotal();

document
  .querySelector("#payment-form")
  .addEventListener("submit", handleSubmit);