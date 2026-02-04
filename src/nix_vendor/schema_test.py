from .schema import parse_json, FlakePrefetch

def test_prefetch_gh():
    res = parse_json(FlakePrefetch,
        """{
            "hash": "sha256-/VqmiNdtTY2K9PbZlmLoVJml77/wnJJ9szg3NbHjSLw=",
            "locked": {
                "lastModified": 1769729117,
                "owner": "TypicalFence",
                "repo": "vim.nix",
                "rev": "da7af26671794e042b8db7b5b603d71d98846ab5",
                "type": "github"
            },
            "original": {
                "owner": "TypicalFence",
                "repo": "vim.nix",
                "type": "github"
            },
            "storePath": "/nix/store/y47xipr2ycpr8sj0n3zbw49zw724ffjw-source"
        }""")
    assert isinstance(res, dict)

def test_prefetch_tarball():
    res = parse_json(FlakePrefetch,
        """{
            "hash": "sha256-Uy+G3bG0SD7NZR4uRLf5NWhEhtOSY0ndQMr1WVXGnJk=",
            "locked": {
                "lastModified": 1769644482,
                "narHash": "sha256-Uy+G3bG0SD7NZR4uRLf5NWhEhtOSY0ndQMr1WVXGnJk=",
                "type": "tarball",
                "url": "https://ftp.gnu.org/pub/gnu/gettext/gettext-1.0.tar.gz"
            },
            "original": {
                "type": "tarball",
                "url": "https://ftp.gnu.org/pub/gnu/gettext/gettext-1.0.tar.gz"
            },
            "storePath": "/nix/store/kcswbs1azwffcmdfknw5a4ql31j3zf87-source"
        }""")
    assert isinstance(res, dict)


