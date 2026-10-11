from src.challenge import ddos_guard_challenge_in_html

DDG_CHALLENGE_HTML = """
<html data-ddg-origin="true" data-ddg-l10n="true">
<head>
  <link rel="stylesheet" href="/.well-known/ddos-guard/js-challenge/index.css">
  <script defer src="/.well-known/ddos-guard/js-challenge/view.js"></script>
  <script defer src="/.well-known/ddos-guard/js-challenge/index.js"></script>
  <script src="https://check.ddos-guard.net/check.js"></script>
</head>
<body>
  <h1 id="ddg-l10n-title">Checking your browser before accessing
    <span class="ddg-origin">annas-archive.gl</span>
  </h1>
  <p id="ddg-l10n-description">Please wait a few seconds.</p>
</body>
</html>
"""

DDG_CHALLENGE_SINGLE_QUOTED = """
<html data-ddg-origin='true'>
<script src="https://check.ddos-guard.net/check.js"></script>
</html>
"""


def test_ddos_guard_challenge_html_is_detected():
    assert ddos_guard_challenge_in_html(DDG_CHALLENGE_HTML) is True


def test_ddos_guard_challenge_accepts_single_quoted_origin():
    assert ddos_guard_challenge_in_html(DDG_CHALLENGE_SINGLE_QUOTED) is True


def test_normal_page_is_not_ddos_guard_challenge():
    html = """
    <html><head><title>Anna's Archive</title></head>
    <body><h1>Search</h1><p>Books, papers, and more.</p></body></html>
    """
    assert ddos_guard_challenge_in_html(html) is False


def test_bare_ddos_guard_mention_is_not_a_challenge():
    html = """
    <html><body>
      Protected by <a href="https://ddos-guard.net">DDoS-Guard</a>.
      Server: ddos-guard
    </body></html>
    """
    assert ddos_guard_challenge_in_html(html) is False


def test_disabled_ddg_origin_without_scripts_is_not_a_challenge():
    html = '<html data-ddg-origin="false"><body>Custom service page</body></html>'
    assert ddos_guard_challenge_in_html(html) is False


def test_origin_alone_without_challenge_scripts_is_not_a_challenge():
    html = '<html data-ddg-origin="true"><body>No challenge scripts</body></html>'
    assert ddos_guard_challenge_in_html(html) is False


def test_script_alone_without_origin_is_not_a_challenge():
    html = (
        "<html><script src="
        '"https://check.ddos-guard.net/check.js"></script></html>'
    )
    assert ddos_guard_challenge_in_html(html) is False


def test_cloudflare_interstitial_is_not_ddos_guard_challenge():
    html = """
    <html><head><title>Just a moment...</title></head>
    <body>
      <div id="cf-spinner-please-wait">Please wait...</div>
      <input name="cf-turnstile-response" type="hidden" value="">
    </body></html>
    """
    assert ddos_guard_challenge_in_html(html) is False
