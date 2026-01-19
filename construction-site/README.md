# Monty Construction Website

A professional, modern construction company website built with HTML5, CSS3, and vanilla JavaScript.

## Features

- **Fully Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Modern UI/UX**: Clean, professional design with smooth animations and transitions
- **Interactive Elements**: Smooth scrolling, mobile menu, form validation, and more
- **SEO Optimized**: Proper semantic HTML and meta tags
- **Performance Optimized**: Lightweight code with fast loading times
- **Easy to Customize**: Well-organized code structure with CSS variables

## Sections

1. **Hero Section**: Eye-catching introduction with call-to-action buttons
2. **Services**: Showcase of 6 construction services with icons
3. **Projects**: Featured project gallery with hover effects
4. **Why Choose Us**: Statistics and key differentiators
5. **About**: Company information and values
6. **Testimonials**: Client reviews and feedback
7. **Contact**: Contact form and information
8. **Footer**: Links, social media, and additional information

## File Structure

```
construction-site/
├── index.html          # Main HTML file
├── css/
│   └── style.css       # Main stylesheet with all styles
├── js/
│   └── main.js         # JavaScript for interactivity
└── images/             # Image assets folder
    ├── hero-bg.jpg     # Hero section background
    ├── about-placeholder.jpg
    └── project-placeholder-[1-4].jpg
```

## Getting Started

### Prerequisites

- A modern web browser (Chrome, Firefox, Safari, Edge)
- A text editor (VS Code, Sublime Text, etc.)
- Optional: A local web server (Live Server extension for VS Code, Python's http.server, etc.)

### Installation

1. Clone or download this repository
2. Navigate to the `construction-site` folder
3. Open `index.html` in your web browser, or use a local server:

   **Using VS Code Live Server:**
   - Right-click on `index.html`
   - Select "Open with Live Server"

   **Using Python:**
   ```bash
   cd construction-site
   python -m http.server 8000
   # Then visit http://localhost:8000
   ```

   **Using Node.js:**
   ```bash
   npx http-server construction-site
   ```

## Customization Guide

### 1. Update Company Information

Edit `index.html` to update:
- Company name (replace "Monty Construction")
- Contact information (phone, email, address)
- Business hours
- Social media links

### 2. Customize Colors

Edit the CSS variables in `css/style.css`:

```css
:root {
    --primary-color: #ff6b35;      /* Main brand color */
    --secondary-color: #f7931e;    /* Secondary brand color */
    --dark-color: #1a1a1a;         /* Dark text/backgrounds */
    --light-color: #f4f4f4;        /* Light backgrounds */
}
```

### 3. Add Your Images

Replace the placeholder images in the `images/` folder:
- `hero-bg.jpg` - Hero section background (1920x1080px recommended)
- `about-placeholder.jpg` - About section image (800x600px recommended)
- `project-placeholder-1.jpg` through `project-placeholder-4.jpg` - Project images (800x600px recommended)

### 4. Update Services

In `index.html`, find the "Services Section" and modify the service cards:
- Change icons (use Font Awesome icon classes)
- Update titles and descriptions
- Add or remove service cards as needed

### 5. Add Real Projects

Update the "Projects Section" in `index.html`:
- Replace placeholder images with actual project photos
- Update project titles and descriptions
- Add more project cards by copying the `.project-card` div

### 6. Modify Testimonials

Edit the testimonials in the "Testimonials Section":
- Update client names and testimonials
- Add or remove testimonial cards
- Include real client photos (optional)

### 7. Configure Contact Form

The contact form currently uses client-side validation only. To make it functional:

**Option 1: Using Formspree (Easiest)**
```html
<form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
```

**Option 2: Using Netlify Forms**
```html
<form name="contact" method="POST" data-netlify="true">
```

**Option 3: Custom Backend**
- Modify the `initContactForm()` function in `js/main.js`
- Connect to your backend API endpoint
- See the commented code example in the file

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Dependencies

- **Font Awesome 6.4.0** - For icons (loaded from CDN)
- No JavaScript frameworks required - pure vanilla JS

## Performance Features

- Lazy loading for images and animations
- Optimized CSS with minimal reflows
- Smooth scroll behavior
- Intersection Observer API for efficient scroll animations
- Mobile-first responsive design

## Accessibility

- Semantic HTML5 elements
- ARIA labels for interactive elements
- Keyboard navigation support
- Alt text for images
- Sufficient color contrast ratios
- Responsive typography

## SEO Features

- Semantic HTML structure
- Meta descriptions and keywords
- Open Graph tags ready (add as needed)
- Clean URL structure
- Fast loading times

## Future Enhancements

Consider adding these features as you grow:

1. **Blog Section**: Share construction tips and company news
2. **Project Details Pages**: Individual pages for each project
3. **Client Portal**: Login area for clients to track projects
4. **Online Estimates**: Calculator for project cost estimates
5. **Gallery Filtering**: Filter projects by category
6. **Video Integration**: Add project walkthrough videos
7. **Live Chat**: Real-time customer support
8. **Multi-language Support**: Reach a broader audience
9. **CMS Integration**: WordPress, Contentful, or custom CMS
10. **Analytics**: Google Analytics or similar tracking

## Deployment

### GitHub Pages
1. Push code to GitHub repository
2. Go to Settings > Pages
3. Select branch and folder
4. Your site will be live at `https://username.github.io/repo-name/`

### Netlify
1. Sign up at netlify.com
2. Drag and drop the `construction-site` folder
3. Site goes live instantly with free HTTPS

### Traditional Hosting
1. Upload files via FTP to your web host
2. Ensure `index.html` is in the root directory
3. Configure domain settings as needed

## Maintenance Tips

1. **Regular Updates**:
   - Keep project portfolio current
   - Update testimonials regularly
   - Refresh images periodically

2. **Content Updates**:
   - Blog posts (if added)
   - News and announcements
   - Service offerings

3. **Technical Maintenance**:
   - Check all links regularly
   - Test contact form submissions
   - Monitor site performance
   - Keep dependencies updated

## Support

For questions or issues with this template:
- Check the code comments in the files
- Review this README thoroughly
- Inspect browser console for JavaScript errors

## License

This website template is created for Monty Construction. Feel free to modify and customize it according to your needs.

## Credits

- Design and Development: Custom built
- Icons: Font Awesome
- Fonts: System fonts (Segoe UI, etc.)

---

**Built with ❤️ for Monty Construction**

Version 1.0.0 | Last Updated: 2024
