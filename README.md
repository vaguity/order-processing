# Misen manual order processing for Fosdick Fulfillment

- for people who bought the 10 and 12 inch bundle and then added on the 8 inch, combine into the 8-10-12 bundle SKU
- combine SKUs into bundles wherever possible

## Combining carbon steel SKUs

The carbon steel skus you should see in the file are:

    MK-2211 (8")
    MK-2212 (10")
    MK-2213 (12")
    MK-2215 (10+12)
    MK-2217 (8+10+12, All 3)
    MK-6300 (seasoning stick - every order should have one of these)
    MK-6301 (seasoning puck)
    Knife skus that were add-ons

The scenarios we are solving for are:

    Customer with MK-2215 and added MK-2211 > Should be changed to MK-2217
    Customer with MK-2212 and added MK-2213 > Should be changed to MK-2215
    Customer with MK-2213 and added MK-2212 > Should be changed to MK-2215
    Customer who individually had MK-2211, MK-2212 and MK-2213 > Should be changed to MK-2217 (there shouldn't be very many of these)

### Notes

- Adjusted name split
