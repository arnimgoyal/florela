const fs = require('fs');

let config = JSON.parse(fs.readFileSync('/Users/admin/GithubProjects/landing-pages/florela/site-config.json', 'utf8'));
let originalConfig = JSON.parse(JSON.stringify(config));
let pendingProductImage = null;

let data = {
    name: 'Test Product',
    description: 'Test Description',
    categoryId: 'bouquets',
    imageAlt: 'Test Alt',
    active: true,
};

const id = 'prod-' + Date.now().toString(36);
const image = pendingProductImage || 'images/cat-bouquets.jpg';
config.products.push({ id, ...data, image });

console.log('Products after add:', config.products.length);

function saveOverrides() {
  const overrides = {};
  overrides.images = {};
  config.images.forEach((img, i) => {
    const orig = originalConfig.images[i];
    if (img.src !== orig.src || img.alt !== orig.alt) {
      overrides.images[img.id] = { src: img.src, alt: img.alt };
      img._modified = true;
    }
  });
  overrides.categories = config.categories;
  overrides.products = config.products;
  overrides.siteSettings = config.siteSettings;
  overrides.heroSection = config.heroSection;
  overrides.storySection = config.storySection;
  overrides.aboutSection = config.aboutSection;
  overrides.ctaSection = config.ctaSection;
  overrides.collectionSection = config.collectionSection;
  overrides.orderSectionHeader = config.orderSectionHeader;
  overrides.orderSteps = config.orderSteps;
  
  // simulation of stringify
  const str = JSON.stringify(overrides);
  console.log('Saved length:', str.length);
}

saveOverrides();
