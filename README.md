# Measure

Quantify and categorize city bike networks.

## Administration tasks

Administration tasks are being provided as convenience in a `justfile`.

More information about [Just] can be find in their repository. The
[installation](https://github.com/casey/just#installation) section of their
documentation will guide you through the setup process.

Run `just -l` to see the list of provided tasks.

## Project structure

- data: stores the shapefiles (_not to be commited_) to process
- docs: the Sphinx documentation of the project
- measure: project source code
- notebooks: notebooks relevant to the project
- results: stores the results of the operations
- tests: project unit tests

## Contributing

Setup the conda environment:

```bash
just
```

This will create or update the environment and display the instructions to
activate/deactivate it.

Then, place the shape files to process in the `data` directory. For now, only
the files ending with `neighborhood_ways.zip` will be detected. The shape files
must be retrieved from the [bna] site.

For instance, for the city of Austin, TX:

1. Go to
   <https://bna.peopleforbikes.org/#/places/02fa7cef-bfb9-494e-9ae9-cdbaeb15f11f/>
2. Click the "Download" button
3. Click "Neighborhood Ways (shp)"
4. Save it into the `data` directory

Finally, run the project to process the file(s):

```bash
python measure/main.py
```

[bna]: https://bna.peopleforbikes.org
[just]: https://github.com/casey/just
