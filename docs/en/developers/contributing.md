# Contributing

> Our small team truly appreciates every contribution made by our community: user stories, feature requests, bug reports, and especially pull requests! If you have _any_ questions please reach out to our Core team at [AceCentre](https://acecentre.org.uk).

## User stories

So you use RelayKeys? Like what we are doing? Got a real problem that needs fixing but don't understand all this code stuff? Please [get in touch](https://acecentre.org.uk/contact/). We will try and help — but please note: **this is very much an open source, fundraised project**. If you can, please consider donating to the project.

## RelayKeys Repository

### [acecentre/relaykeys](https://github.com/acecentre/relaykeys)

The project is written in Go. A quick overview of the contents:

- **cmd/relaykeys-daemon/** — daemon entry point + Windows service support (`kardianos/service`)
- **cmd/relaykeys-cli/** — CLI client for AAC software (Grid 3, Communicator 5, etc.)
- **cmd/relaykeys-tray/** — Windows system tray app (`getlantern/systray`)
- **cmd/relaykeys-menubar/** — macOS menu bar app (Cocoa, requires CGo)
- **internal/blehid/** — AT command protocol over serial + HID keycode map
- **internal/capture/** — Event type and `IsModifier()` helper
- **internal/config/** — INI config file loading
- **internal/keymap/** — JSON keymap loading (US, UK, DE, FR, ES, IT)
- **internal/macro/** — Macro save/load/record/replay
- **internal/rpc/** — JSON-RPC server (port 5383) + client
- **internal/serial/** — Hardware serial via `go.bug.st/serial`, auto-detect by VID/PID
- **internal/simulator/** — Full firmware simulator for testing
- **internal/webui/** — Embedded web UI (HTML/JS/CSS) + WebSocket hub
- **keymaps/** — JSON keyboard layout files
- **docs/** — Documentation (GitBook)
- **archive/** — Old Python source (reference only)

## Development Setup

1. Install [Go 1.21+](https://go.dev/dl/)
2. Clone the repo: `git clone https://github.com/acecentre/relaykeys.git`
3. Build: `go build ./...`
4. Test: `go test ./... -count=1`
5. See [building-a-binary.md](building-a-binary.md) for full build instructions

## Simple Pull Requests

Before we get into the full-blown "proper" way to do a pull request, let's quickly cover an easier method you can use for _small_ fixes. This way is especially useful for fixing quick typos in the docs, but is not as safe for code changes since it bypasses validation and linting.

1. Sign in to GitHub
2. Go to the file you want to edit (eg: [this page](https://github.com/acecentre/relaykeys/docs/blob/master/feature-requests.md))
3. Click the pencil icon to "Edit this file"
4. Make any changes
5. Describe and submit your changes within "Propose file change"

That's it! GitHub will create a fork of the project for you and submit the change to a new branch in that fork. Just remember to submit separate pull requests when solving different problems.

## Proper Pull Requests

_Loosely based on_ [_this great Gist_](https://gist.github.com/Chaser324/ce0505fbed06b947d962) _by_ [_Chaser324_](https://gist.github.com/Chaser324)

We like to keep a tight flow when working with GitHub to make sure we have a clear history and accountability of what changes were made and when. Working with Git, and especially the GitHub specific features like forking and creating pull requests, can be quite daunting for new users.

To help you out in your Git(Hub) adventures, we've put together the (fairly standard) flow of contributing to an open source repo.

### Forking the repo

Whether you're working on the daemon, CLI, or web UI, you will need to have your own copy of the codebase to work on. Head to the repo of the project you want to help out with and hit the Fork button. This will create a full copy of the whole project for you on your own account.

To work on this copy, you can install the project locally according to the normal installation instructions, substituting the name `acecentre` with the name of your github account.

### Keeping your fork up to date

If you're doing more work than just a tiny fix, it's a good idea to keep your fork up to date with the "live" or _upstream_ repo. This is the main acecentre repo that contains the latest code. If you don't keep your fork up to date with the upstream one, you'll run into conflicts pretty fast. These conflicts will arise when you made a change in a file that changed in the upstream repo in the meantime.

#### On git remotes

When using git on the command line, you often pull and push to `origin`. You might have seen this term in certain commands, like

```bash
git push origin master
```

or

```bash
git pull origin new-feature
```

In this case, the word `origin` is referred to as a _remote_. It's basically nothing more than a name for the full git url you cloned the project from:

```bash
git push origin master
```

is equal to

```bash
git push git@github.com:username/repo.git master
```

A local git repo can have multiple remotes. While it's not very common to push your code to multiple repos, it's very useful when working on open source projects. It allows you to add the upstream repo as another remote, making it possible to fetch the latest changes straight into your local project.

```bash
# Add 'upstream' to remotes
git remote add upstream git@github.com:acecentre/relaykeys.git
```

When you want to update your fork with the latest changes from the upstream project, you first have to fetch all the (new) branches and commits by running

```bash
git fetch upstream
```

When all the changes are fetched, you can checkout the branch you want to update and merge in the changes.

```
git checkout master
git rebase upstream/master
```

If you haven't made any commits on the branch you're updating, git will update your branch without complaints. If you _have_ created commits in the meantime, git will step by step apply all the commits from _upstream_ and try to add in the commit you made in the meantime. It is very plausible that conflicts arise at this stage. When you've changed something that also changed on the upstream, git requires you to resolve the conflict yourself before being able to move on.

### Doing Work

Whenever you begin working on a bugfix or new feature, make sure to create a new branch. This makes sure that your changes are organized and separated from the master branch, so you can submit and manage your pull requests for separate fixes/features more easily.

```bash
# Checkout the master branch - you want your new branch to come from master
git checkout master

# Create a new branch named newfeature (give your branch its own simple informative name)
git branch newfeature

# Switch to your new branch
git checkout newfeature
```

### Submitting a Pull Request

Prior to opening your pull request, you might want to update your branch a final time, so it can immediately be merged into the master branch of upstream.

```bash
# Fetch upstream master and merge with your repo's master branch
git fetch upstream
git checkout master
git merge upstream/master

# If there were any new commits, rebase your master branch
git checkout newfeature
git rebase master
```

Once you've committed and pushed all the changes on your branch to your fork on GitHub, head over to GitHub, select your branch and hit the pull request button.

You can still push new commits to a pull request that already has been opened. This way, you can fix certain comments reviewers might have left.

## Feature Requests

### 80/20 Rule

The main thing to be aware of when submitting a new acecentre feature request, is our rule on edge-cases. To keep the acecentre core codebase as clean and simple as possible we will only consider adding features that at least 80% of our user-base will use. If we feel that less than 80% of our users will find the feature valuable then we will not implement it. Instead, those edge-case features should be added as Extensions.

### Browsing Existing Requests

Before adding a new request, you should also first [search](https://github.com/acecentre/relaykeys/issues?q=is%3Aissue+is%3Aopen+sort%3Areactions-%2B1-desc) to see if it has already been submitted. All feature requests should include the `enhancement` label, so you can filter by that. And remember to also check _closed_ issues since your feature might have already been submitted in the past and either rejected or already implemented.

Also, if you want to see the most highly requested features you can sort by `:+1:` (the thumbs-up emoji).

### Submitting a Request

If your idea passes the 80/20 test and has not already been submitted, then we'd love to hear it! Submit a new issue using the Feature Request template and be sure to include the `enhancement` label. It's important to completely fill out the template with as much useful information as possible so that we can properly review your request. If you have screenshots, designs, code samples, or any other helpful assets be sure to include those too!

### Voting on Requests

You can also vote on existing feature requests. As mentioned above, the `:+1:` and `:-1:` are used for sorting, so adding one of these reactions to the GitHub issue will cast a vote that helps us better identify the most desired (or undesired) features. And remember to add a comment if you have additional thoughts to help clarify or improve the request.

### Fulfilling a Request

Our core team is always working hard to implement the most highly-requested community features, but we're a small team. If you need the feature faster than we can provide it, or simply want to help improve the acecentre platform, we'd love to receive a pull-request from you!
