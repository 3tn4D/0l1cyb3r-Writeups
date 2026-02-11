const CryptoJS = require("crypto-js");

function AES_decrypt(message = 'U2FsdGVkX1/JEKDXgPl2RqtEgj0LMdp8/Q1FQelH7whIP49sq+WvNOeNjjXwmdrl', key = 'ML4czctKUzigEeuR') {
  var code = CryptoJS.AES.decrypt(message, key);
  var decryptedMessage = code.toString(CryptoJS.enc.Utf8);
  return decryptedMessage;
}

console.log(AES_decrypt());
