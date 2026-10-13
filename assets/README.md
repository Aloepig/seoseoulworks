# Site assets

Images and fonts are served from this directory on the site's own origin.
Upload `index.html`, root-level `favicon.ico`, and the entire `assets/` directory to the S3 bucket,
preserving the directory structure. Upload assets before replacing index.html.
The `tools/` directory does not need to be uploaded.

After uploading, invalidate `/*` in CloudFront if cached content remains.
Check both images and fonts in the browser after deployment.

`images/og-image.png` is the 1200 x 630 social sharing card referenced by the
Open Graph and Twitter card metadata in index.html. Upload it before the HTML.
To regenerate it on Windows with Pillow installed, run
`python tools/create_og_image.py`. This uses the installed Malgun Gothic fonts
and the site's existing S icon. Sharing services may cache previews separately
from CloudFront; previously shared links may need a preview cache refresh.

## Sources

- Hero: https://images.unsplash.com/photo-1455390582262-044cdead277a
- About: https://images.unsplash.com/photo-1519682337058-a94d519337bc
- Fonts: Google Fonts DM Sans, Noto Sans KR, and Noto Serif KR.
- The fonts' SIL Open Font License texts are included in `fonts/*-OFL.txt`.

The font CSS retains Unicode ranges, so browsers request the subsets needed
for the page's characters rather than downloading all font files at once.
Full language subsets are retained to support future Korean content changes.

To download the assets again, run `python tools/vendor_assets.py` with network
access from the project directory. Normal site visits need no connection to
Google Fonts or Unsplash.
