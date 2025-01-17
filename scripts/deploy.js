import ghpages from 'gh-pages';

ghpages.publish('dist', {
    dotfiles: true,
    message: 'Deploy to GitHub Pages'
}, function(err) {
    if (err) {
        console.error('Deployment failed:', err);
        process.exit(1);
    } else {
        console.log('Deployed successfully!');
    }
});
