<?php
session_start(['use_strict_mode' => 1]);
session_destroy();

header('Location: /');
exit();
