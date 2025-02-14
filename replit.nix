{ pkgs }: {
    deps = [
        pkgs.python310
        pkgs.python310Packages.pip
        pkgs.python310Packages.flask
        pkgs.python310Packages.requests
        pkgs.python310Packages.gunicorn
        pkgs.redis
    ];
    env = {
        PYTHONBIN = "${pkgs.python310}/bin/python3.10";
        LANG = "en_US.UTF-8";
    };
}