# LibreCores CI Github Action with FuseSoC

This executes FuseSoC in the [LibreCores CI docker
container](https://github.com/librecores/ci-docker-image).

It is still in an early development phase, please feel free to open an issue
with your suggestion!

## Inputs

### `arguments`

Those are the main arguments. It can also be used to run FuseSoC without setting
any other of the inputs, despite that is discouraged.

### `command`

Command to execute, such as `build`, `run` etc.

### `command-arguments`

Arguments to be passed to the command.

### `core`

The core/system identifier to execute on.

### `core-arguments`

Arguments to be passed to the core.

### `target`

Override default target, default none.

### `tool`

Override default tool for target, default none.

## Example usage

```yaml
uses: librecores/ci-fusesoc-action@2020.6-rc1
with:
  core: myorg:mylib:mycore
  flow: run
  target: lint
```
