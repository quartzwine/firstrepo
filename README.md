# firstrepo
hacking away at the base blockchain and eventually friends.tech

currently trying to create a local db to hold block data which i can query against. essentially i want a mini dune


why dont i use dune? data is ~2hrs late. not recent enough for my use case

## deps
this package uses sqllite as a db. upgrade to something more hardcore if you wish.

base is about 32kb per block. one day of blocks is about 1gb. sqllite should be sufficient


## getting started
1) add ur API key from quicknode into a .env file. `API_KEY`


## queries

get friend.tech addresses which bought their own shares
```
SELECT '0x' || substr(input,35,40) AS address from transactions
WHERE to_address = '0xcf205808ed36593aa40a44f10c7f7c2f67d4a4d4'
AND SUBSTR(input, 1, 10) = '0x6945b123'
AND '0x' || substr(input,35,40) = from_address;
```
