// Controls the opening and closing of the booking modal
document.addEventListener('DOMContentLoaded', (event) => {
    const modal = document.getElementById('bookingModal');
    const btn = document.getElementById('bookEventBtn');
    const span = document.getElementsByClassName('close')[0];
    btn.onclick = function () {
        modal.style.display = 'block';
    }
    span.onclick = function () {
        modal.style.display = 'none';
    }
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
});


// Controls how the booking cards are displayed
// in the user profile
document.addEventListener("DOMContentLoaded", function () {
    const bookingList = document.getElementById("booking-list");
    const bookingCards = bookingList.querySelectorAll(".booking-card");

    if (bookingCards.length % 2 !== 0) {
        // If the number of booking cards is odd
        const lastCardIndex = bookingCards.length - 1;
        bookingCards[lastCardIndex].classList.add("center-last-card");
    }
});


// Function that handles downloading of booked event tickets
function downloadTicket(bookingId, eventTitle, eventDate, bookingIdText, userName) {
    const ticketCanvas = document.createElement('canvas');
    ticketCanvas.width = 350;
    ticketCanvas.height = 200;
    const ticketContext = ticketCanvas.getContext('2d');

    // Draw background color
    ticketContext.fillStyle = '#002E5D';
    ticketContext.fillRect(0, 0, ticketCanvas.width, ticketCanvas.height);

    // Draw text content
    ticketContext.fillStyle = 'white';
    ticketContext.font = 'bold 16px Arial';
    ticketContext.fillText('EventsPro', 20, 30);
    ticketContext.font = 'bold 14px Arial';
    ticketContext.fillText(eventTitle.toUpperCase(), 80, 60);
    ticketContext.font = '14px Arial';
    ticketContext.fillText(`Booking ID: ${bookingIdText}`, 20, 90.5);
    ticketContext.fillText(`Date: ${eventDate}`, 20, 110.5);
    ticketContext.fillText(`Name: ${userName}`, 20, 130.5);

    // Draw QR code
    const qrCodeImage = new Image();
    qrCodeImage.crossOrigin = 'Anonymous';
    qrCodeImage.onload = () => {
        ticketContext.drawImage(qrCodeImage, ticketCanvas.width - 100, ticketCanvas.height - 100, 80, 80);
        // Convert canvas to data URL and download
        const dataURL = ticketCanvas.toDataURL('image/png');
        const link = document.createElement('a');
        link.href = dataURL;
        link.download = `${eventTitle}_ticket.png`;
        link.click();
    };
    qrCodeImage.onerror = (error) => {
        console.error('Error loading QR code:', error);
    };
    qrCodeImage.src = `http://localhost:8000/fetch-qr-code/${bookingId}/`;
}