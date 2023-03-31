# MPIA Conference website template

This repository contains a website generator that can make your conference website.

It generates the content of the web pages from markdown documents stored in `docs/content`.

The content files contain markdown with metadata information, i.e., a front matter delimited by `---`. Sometimes they provide only metadata information (e.g., `index.`md`). The metadata information follows the Yaml syntax.


## Provided content

Most of the content files have a metadata entry `type: section`

* The main index page for your website: `docs/content/index.md`
   * It contains the primary information about your event (title, dates, etc.)
   * the `content` list contains which files will be included and their ordering. (if their header contains `active: true`)

* A typical code of conduct: `docs/content/code-of-conduct.md`
   * MPIA strongly recommends stating the code of conduct of your event clearly. You may want to update the example we provide.

* We provide an example of a typical logistics section with `docs/content/logistics.md`
   * it describes childcare service, information about lunch, conference dinner, and accomodation, for instance.

* We provide a template for travel information
   * to MPIA in `docs/content/travel-mpia.md`
   * to Ringberg in `docs/content/travel-ringberg.md`

* We provide a template for venue information
   * `docs/content/venue-hda.md`
   * `docs/content/venue-ringberg.md`

* If you want to list some speakers or participants with pictures and information (for instance, teachers or review talks), you can use the `type:speakers` layout. An example in `docs/content/speakers.md`
   * This file lists speakers in the metadata, and the generator will take care of the rendering

* The schedule is also a particular layout `type`:schedule`, an example is provided in `docs/content/programme.md`