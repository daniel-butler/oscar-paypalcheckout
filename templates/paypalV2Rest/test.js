onApprove: function(data) {
      return fetch('http://127.0.0.1:8000/paypal/capture-paypal-transaction', {
        method: "POST",
        headers: {
          'content-type': 'application/json',
           "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
          orderID: data.orderID
        })
      }).then(function(res) {
        return res.json();
      }).then(function(details) {
        console.log(details);
        alert('Transaction funds captured from ' + details.payer_given_name);
        post('/', {name: 'Johnny Bravo'});
      })
    }


    onApprove: function(data) {

        post('/', {name: 'Johnny Bravo'});

    }