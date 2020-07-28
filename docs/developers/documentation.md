# Documentation

## Introduction

The docs are using [VuePress](http://vuepress.vuejs.org) - and the code for the docs is found in the ``docs`` directory

## Setup

1. Install [NodeJS](https://nodejs.org/en/)
2. Open up a console/terminal and install VuePress. i.e. ``npm install vuepress``
3. Navigate in your console to where the relaykeys directory is. e.g. ``cd relaykeys``
4. Run the development version of VuePress e.g. ``vuepress dev docs``


## Quick tour of where to find the files

See ``docs/.vuepress/.config`` for config settings

all other files are markdown documents. 

## Pushing changes to the hosted site

Once you are ready we use ``docs-deploy.sh`` to deploy the site to GitHub pages