# |{"username" : Am | ministratore |, "registration_date" : str(datetime.date.today())}
# |                 |              |
# |    blocco 1     |   blocco 2   |

# register(Am)
token1 = "dc9a9174a06faf1deae74f0062250aae71ec192b73c85a5d6c3a348d851cd158ed82c69afada03372dcb0c705ce817c1496dae538bebe9789e76312d66203d29"[:32]
#         ^                               ^
#         |                               |

# register(  ministratore)
token2 = "c263bbf95e39896e5375cbbd8e49fd9a7f4e3060e6ac4664ef6f1c2c7de699f300c1aa6a161f582cbccf8563bef5b1bfbeb32be6c7ce6c799a02daa54d40604fc7e8099423da78b60246d3c8251ef7eb"[32:]
#                                         ^                                                                                                                              ^
#                                         |                                                                                                                              |

token3 = "dc9a9174a06faf1d5375cbbd8e49fd9a7f4e3060e6ac4664ef6f1c2c7de699f300c1aa6a161f582cbccf8563bef5b1bfbeb32be6c7ce6c799a02daa54d40604fc7e8099423da78b60246d3c8251ef7eb"

print(token1 + token2)