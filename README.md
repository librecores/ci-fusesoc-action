# LibreCores CI Github Action with FuseSoC

This executes FuseSoC in the [LibreCores CI docker container](https://github.com/librecores/ci-docker-image).

It is still in an early development phase, please feel free to open an issue with your suggestion!

## Inputs

### `core`

**Required** The core/system identifier to execute on.

### `flow`

**Required** Command to execute, such as `build`, `run` etc.

### `target`

*Optional* Override default target, default none.

### `tool`

*Optional* Override default tool for target, default none.

## Example usage

```yaml
uses: librecores/ci-fusesoc-action@2020.6-rc1
with:
  core: myorg:mylib:mycore
  flow: run
  target: lint
```
