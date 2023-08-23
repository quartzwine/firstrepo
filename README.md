# firstrepo
hacking away at the base blockchain and eventually friends.tech

currently trying to create a local db to hold block data which i can query against. essentially i want a mini dune


why dont i use dune? data is ~2hrs late. not recent enough for my use case

## deps
~~this package uses sqllite as a db. upgrade to something more hardcore if you wish.~~

yup so sqllite wasn't good enough. this now uses postgres.
so the issue with sqlite is its pretty garbo at concurrent reads/writes. it can handle the writes, but 
i have a separate service trying to read at the same time and that does not work.


base is about 32kb per block. one day of blocks is about 1gb.


## getting started
1) add ur API key from quicknode into a .env file. `API_KEY`
2) you'll prolly need to change quicknode url as well.
3) add `DB_PASS` to ur .env. set this up with postgres so yeah u know what to do
4) run `populate.py`. will start adding recent blocks from base chain to postgres. 
5) `main.py` dont use this its a wip



## known bugs.
sometimes service dies when requesting from `get_transaction_data`. connection timeout error.
tried to add tenacity but also breaks

## queries

get friend.tech addresses which bought their own shares
```
SELECT '0x' || substr(input,35,40) AS address from transactions
WHERE to_address = '0xcf205808ed36593aa40a44f10c7f7c2f67d4a4d4'
AND SUBSTR(input, 1, 10) = '0x6945b123'
AND '0x' || substr(input,35,40) = from_address;
```


## future plans
- seems a bit overbearing i prolly went overkill. want to simplify this and see if i can run on rbpi