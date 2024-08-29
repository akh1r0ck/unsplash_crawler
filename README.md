# unsplash_crawler

## Requirements

Access [unsplash developer page](https://unsplash.com/developers) to create apps and get API key.

## Example

```python
unsplash_key = os.getenv("UNSPLASH_KEY")
query = "pattern"
crawl_unsplash(
    unsplash_key, 
    query=query, num_photos=1000, per_page=30
    )
```
