# pytorch-rwa

This project is meant to be a pytorch implementation of the paper [here](https://arxiv.org/pdf/1703.01253.pdf)

So far the Add task works! I've also added a decay term that may need to be modified but still 
seems to work nevertheless.

I've also added a new cell that looks like a CGRU cell from the Neural GPU but differs slightly in that I use groups.
Take a look!

TODO:
- [ ] Train the network on all tasks in [the original repo](https://github.com/jostmey/rwa)
    - [x] Implemented AddTask
- [ ] Use this in projects!