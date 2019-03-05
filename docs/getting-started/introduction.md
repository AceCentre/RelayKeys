# 🐰 Welcome to the Directus Docs!

> These Docs will help get you up-and-running quickly, guide you through advanced features, and explain the concepts that make Directus so unique.

## What is Directus?

**Directus is an open-source suite of software for managing content in custom databases.** It instantly wraps SQL databases with a dynamic API and provides a safe and intuitive Admin App for non-technical users. It can be used as a headless CMS for managing project content, a database client for modeling and viewing raw data, or as standalone software to replace other costly services.

Yes, this is a very broad description. Directus is a simple solution for complex problems.

### What is a "headless" CMS?
With _traditional_ CMS you choose a design template, throw in some content, and it generates a blog or simple website. However that means that these platforms are limited to websites only, since your designs and content are all jumbled together.

In a "headless" CMS, there are no templates built-in, no design or layout editor, and it doesn't generate a website (aka the "head"). It only manages _content_. That's it. Now that your content is cleanly decoupled, you can connect it anywhere! Websites, sure, but also native apps, kiosks, digital signage, other software, internet-of-things (IoT) devices, or any other data-driven project.

In short: traditional CMS are for small or medium-sized websites, headless CMS can manage content for anything.

### What is a "database wrapper"?
Our database-wrapper uses the SQL database's schema to dynamically build a set of custom API endpoints based on the custom achitecture. This means you can install it on top of existing databases, tailor actual database tables/columns to specific project requirements, and even build/optimize in the database directly. 

Perhaps one of the biggest advantages of using a database-wrapper like ours in your project, is that you always have direct access to your pure and unaltered data. Meaning, you can always bypass the API, SDK, or CMS and connect to data directly — effectively removing _any_ bottleneck or additional latency.

## Core Principles

Every aspect of Directus is data-first and guided by the following core principles:

* **Agnostic** — Directus is not specific to websites or limited to HTML. Your data is compatible with any platform or device so you can connect it to all of your projects.
* **Extensible** — Directus can not be outgrown. Every aspect of the toolkit is modular, allowing you to adapt, customize, and extend the Core feature-set.
* **Limitless** — Directus does not impose any arbitrary restrictions or limits. Add as many users, roles, locales, collections, items, or environments as you'd like.
* **Open** — Directus is not a closed, obfuscated, or black-boxed system. Its simple codebase public and transparent so you can audit the data flow from end-to-end.
* **Portable** — Directus does not _lock_ you to its platform or services. You can migrate your data elsewhere at any point — or just delete Directus and connect to your database directly.
* **Pure** — Directus does not alter your data or store it in a predefined or proprietary way. All system data is stored elsewhere, never commingled.
* **Unopinionated** — Directus does not impose any self-proclaimed "best practices". It lets you decide how your data is modeled, managed, and accessed.

## The Directus Ecosystem

There are several properties within the Directus ecosystem, below is a brief overview.

### Directus API

This is the "engine" of Directus, providing a dynamic API for any MySQL database. It is bundled in the Directus Suite but it can also be installed as a standalone framework. The [codebase](https://github.com/directus/api) is written primarily in PHP and uses Zend-DB for database abstraction.

### Directus Application

This is the admin app that allows non-technical users to manage database content. It can be installed as a standalone webapp for multitenancy but must be connected to an instance of the Directus API to function. The [codebase](https://github.com/directus/app) is written in Vue.js.

### Directus Suite

Both the App and API will be needed for most use-cases, so our [main repository](https://github.com/directus/directus) is a combined build that includes the Directus API, Directus App, and all dependencies. This is the recommended method for installing Directus.

### Directus Cloud

Directus is completely free and open-source, but we also offer a [Content-as-a-Service platform](https://directus.cloud/) to help offset our operating costs. The open-source and hosted versions are identical, but our Cloud service offers faster setup, automatic upgrades, and premium support.

### Directus Docs

This is what you're reading right now. We believe that maintaining great Documentation is just as important as releasing great software. Luckily our docs are all written in markdown in a [public repository](https://github.com/directus/docs) so the community can help!

### Directus Demos

To make it as easy as possible to actually play around with Directus we maintain two online demos: [latest release](https://directus.app) (stable) and [latest commit](https://next.directus.app) (canary). Both demos reset each hour so if things look a little screwy just wait a bit.

### Directus Website

For general information, resources, and team info we maintain a marketing [website](https://directus.io/). This is a good non-technical hub to serve as as introduction to the Directus platform.

### Directus Marketplace

Coming in early 2019, this will be a library of extensions available for Directus. Eventually we plan on opening this up to community submissions and allowing monetization — but initially it will showcase free extensions created by our core team.
