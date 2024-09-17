def get_social_news_banner():
    return """
    <style>
    .main-header {
        background: linear-gradient(135deg, #2ecc71, #3498db); /* Green to blue gradient for sustainability */
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.0rem;
        text-align: center;
    }
    .main-header h1 {
        color: white;
        font-size: 2.0rem;
        margin: 0;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
    }
    .main-header p {
        color: #f0f0f0;
        font-size: 0.9rem;
        margin: 0.3rem 0 0 0;
        text-align: center;
    }
    .benefit-pills {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 0.3rem;
        margin-top: 0.6rem;
    }
    .benefit-pill {
        background-color: rgba(255, 255, 255, 0.15);
        color: white;
        padding: 0.3rem 0.5rem;
        border-radius: 20px;
        font-size: 0.85rem;
        backdrop-filter: blur(5px);
    }
    </style>
    <div class="main-header">
        <h1>🌿 Sustainability Reports Guide </h1>
    </div>
    """