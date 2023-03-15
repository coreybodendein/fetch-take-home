# Receipt Processor

## What is it?

This is a Django project with Django Rest Framework that implements the Fetch coding challenge
[here](https://github.com/fetch-rewards/receipt-processor-challenge).

## Getting Started

1. Have [Docker](https://www.docker.com/) installed.
2. Clone this repo.
3. Run `docker build -t corey/receipt-processor .` to build the image.
4. Run `docker run -p 8000:8000 corey/receipt-processor:latest` to run the image.
5. Go to Postman and try to interact with it, e.g.:
   * `POST` to `http://localhost:8000/receipts/process` with a body like:
      ```json
      {
        "retailer": "M&M Corner Market",
        "purchaseDate": "2022-03-20",
        "purchaseTime": "14:33",
        "items": [
          {
            "shortDescription": "Gatorade",
            "price": "2.25"
          },{
            "shortDescription": "Gatorade",
            "price": "2.25"
          },{
            "shortDescription": "Gatorade",
            "price": "2.25"
          },{
            "shortDescription": "Gatorade",
            "price": "2.25"
          }
        ],
        "total": "9.00"
      }
      ```
     and note the `id` in the JSON response.
  * `GET` to `http://localhost:8000/receipts/{id}/points` (Replacing `{id}` with the ID of a receipt returned from the
    `POST` response above)