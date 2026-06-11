{pkgs}: {
  deps = [
    pkgs.redis
    pkgs.sqlite-interactive
    #pkgs.python39Packages.celery
    #pkgs.python39Packages.redis
  ];
}
