# Static Site Generator

A Python static site generator built through the Boot.dev course.

## Local preview

```bash
./main.sh
```

Builds into `docs/` with `/` as the base path, then serves http://localhost:8888/.

## Production build

```bash
./build.sh
```

Builds into `docs/` with `/static-site-generator/` as the base path. GitHub Pages
publishes the committed `docs/` directory from `main` at
https://EthanBalling.github.io/static-site-generator/.

Run `./build.sh` before committing generated files, especially after a local
preview, so the committed pages use the production base path.

## Tests

```bash
./test.sh
```
