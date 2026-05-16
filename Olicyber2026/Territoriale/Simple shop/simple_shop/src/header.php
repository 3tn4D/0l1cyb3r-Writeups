<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <title>Document</title>
</head>

<body>
    <nav class="bg-fuchsia-950 text-white p-4 flex items-center justify-between px-8 py-1 h-16">
        <div>Logo</div>
        <?php if (isset($_SESSION['username'])) { ?>
            <ul class="flex space-x-4" id="menu">
                <li>
                    <a href="/logout.php" class="cursor-pointer hover:underline">Logout</a>
                </li>
            </ul>
        <?php } ?>
    </nav>