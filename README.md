dogmon
======

HTTP log monitoring console program

## Download

Start by cloning the repository:

``` sh
git clone https://github.com/raphaelh/dogmon.git
cd dogmon
```

## Usage

Now, if you run `make`, you will see all the available commands. `make` takes care of all the dependencies, so you don't need to worry about previous steps needed before running a command.

`dogmon` monitors the file `/tmp/access.log` by default. If you don't have a real log file to monitor, you can generate one with the following command:
``` sh
./scripts/generate_log
```

On the first run, it will download a real log from elastic github repository, and convert it to NCSA Common Log Format. Then it will pipe it with a rate limit to `/tmp/access.log` in order to simulate a real-life scenario (it will generate alerts in `dogmon`)

### Run dogmon in the venv

``` sh
make run
```

It will create a venv and run `dogmon` in the venv with default arguments (logfile = `/tmp/access.log` and threshold = 10)

### Run dogmon Docker image

``` sh
make docker-run
```

It will build a Docker image and run it with default arguments for `dogmon`.


## For developers
Don't forget to run `. venv/bin/activate` before working on the project :) If you are inside the venv you should see `(venv)` at the beginning of your prompt.

### Run dogmon with different arguments

You can show the available arguments with `-h` or `--help`:
``` sh
dogmon -h
```

For example, to monitor `/var/log/access.log` with a high traffic threshold of 20 requests per second:
``` sh
dogmon -f /var/log/access.log -t 20
```

### Run code checks

``` sh
make lint
```

### Run all the tests

``` sh
make test
```

## Requirements

* Python >= 3.6
* Docker if you want to run the Docker image

## TODO

* support more web log formats : Combined Log Format (Apache, Nginx), Amazon S3, Elastic Load Balancing, CloudFront, etc) and custom log format strings
* update metrics in realtime
* add support for a configuration file
* customizable layout and color scheme
* metrics per Virtual Host
* generate a report in HTML, JSON or CSV
