def update(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == "POST":
        form = CreateForm(request.data, instance=post, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:detail', pk)
        pass
    else:
        pass 