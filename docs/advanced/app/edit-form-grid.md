# Edit Form Placement

Interfaces on the edit form are layed out using a flex-based system. `directus_fields` has an enum column that controls if the interface has 1, 2, 3, or 4/4s of the row available. The edit form itself has a max width to prevent unusuably wide interfaces.

```
Rows

|------------------------------------------------------------------------------|
|                                       4                                      |
|------------------------------------------------------------------------------|
|                   2                   |                   2                  |
|------------------------------------------------------------------------------|
|                         3                          |           1             |
|------------------------------------------------------------------------------|

```

Next to this automatic flex based grid, we provide you with a few width classes to use on the interface itself:

* `width-x-small`
* `width-small`
* `width-normal`
* `width-large`
* `width-x-large`

These classes should be used as max-width for interfaces that shouldn't be allowed to grow to the full width of the edit form, like text-inputs:

```
Bad

|------------------------------------------------------------------------------|
| [__________________________________________________________________________] |
|------------------------------------------------------------------------------|

Good

|------------------------------------------------------------------------------|
| [__________________]                                                         |
|------------------------------------------------------------------------------|

```

By using one of the provided classes, you'll make sure that your interface aligns nicely with the others.
