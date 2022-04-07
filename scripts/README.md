# Script generator

To generate a load script use the generator at [json-generator](https://json-generator.com)

## Script

```json
[
  '{{repeat(100, 1000)}}',
  {
    request_id: '{{index(1)}}',
    user: '{{random("Vianetta","Daisy","Drew Socks","Sophie\'s Diary Owner","Steve")}}',
    action: '{{random("pet_a_pet","increase_snack_balance")}}',
    value: function(tags) {
      if(this.action === "pet_a_pet")
        return tags.random("Loki","Daisy","Missy","Flick","Java","Gizzy","Mia","Snuffles","Dave","Tweety","Amber","Nagini","Salazar","Garrett the Ferret","Rufus");
      else
        return tags.integer(-10,300);
         
    }
  }
]
```
