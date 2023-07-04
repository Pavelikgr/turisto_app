function logout() {
    fetch('/auth/logout', {
        method: 'POST'
    })
    .then(response => {
        if (response.ok) {
            // Optional: Perform any additional actions after logout
            // For example, redirect to another page
            window.location.href = '/'; // Redirect to the homepage
        } else {
            // Handle error response
            console.log('Error during logout');
        }
    })
    .catch(error => {
        console.log('Error during logout:', error);
    });
}