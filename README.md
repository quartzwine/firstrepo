# firstrepo
hacking away at the base blockchain and eventually friends.tech

currently trying to create a local db to hold block data which i can query against. essentially i want a mini dune


why dont i use dune? data is ~2hrs late. not recent enough for my use case

## deps
this package uses sqllite as a db. upgrade to something more hardcore if you wish.

base is about 32kb per block. one day of blocks is about 1gb. sqllite should be sufficient


## getting started
1) add ur API key from quicknode into a .env file. `API_KEY`


