#!/usr/bin/node
const esbuild = require("esbuild");
const copyStaticFiles = require("esbuild-copy-static-files");

const args = process.argv.slice(2);
const watch = args.includes("--watch");
const build = args.includes("--build");

const loader = {};

const plugins = [
    copyStaticFiles({
        src: "./static",
        dest: "../{{cookiecutter.project_slug}}/statics/",
        dereference: true,
        errorOnExist: false,
        preserveTimestamps: true,
        recursive: true,
    }),
];

const external = ["/fonts/*", "/images/*"];

let options = {
    entryPoints: ["./js/main.ts"],
    outdir: "../{{cookiecutter.project_slug}}/statics/",
    target: "esnext",
    format: 'esm',
    bundle: true,
    sourcemap: true,
    define: {},
    treeShaking: true,
    watch: false,
    external,
    loader,
    plugins,
};

if (watch) {
    options = {
        ...options,
        watch: true,
        sourcemap: "inline",
    };
}

if (build) {
    options = {
        ...options,
        minify: true,
    };
}

const promise = esbuild.build(options);
if (watch) {
    promise.then((result) => {
        process.stdin.on("close", () => {
            process.exit(0);
        });

        process.stdin.resume();
    });
}
