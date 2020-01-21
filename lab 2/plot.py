import os
import numpy as np
import matplotlib.pyplot as plt

def split_name(folder):
    """
    Extract the specs from the given folder name
    """
    params = folder.split('_')

    return [int(p) for p in params]

def get_index(params):
    """
    Get an array-like indexing for the parameters
    """
    idx = []

    if len(params) == 5:
        if params[0] not in [16, 32, 64, 128]:
            raise AttributeError('param 0')
        else:
            idx.append([16, 32, 64, 128].index(params[0]))

        if params[1] not in [1, 2, 4]:
            raise AttributeError('param 1')
        else:
            idx.append([1, 2, 4].index(params[1]))

        if params[2] not in [16, 32, 64, 128]:
            raise AttributeError('param 2')
        else:
            idx.append([16, 32, 64, 128].index(params[2]))

        if params[3] not in [2, 4, 8]:
            raise AttributeError('param 3')
        else:
            idx.append([2, 4, 8].index(params[3]))
        
        if params[4] not in [32, 64, 128]:
            raise AttributeError('param 6')
        else:
            idx.append([32, 64, 128].index(params[4]))
    
    elif len(params) == 3:
        if params[0] not in [256, 512, 1024, 2048, 4096]:
            raise AttributeError('param 4')
        else:
            idx.append([256, 512, 1024, 2048, 4096].index(params[0]))

        if params[1] not in [4, 8, 16]:
            raise AttributeError('param 5')
        else:
            idx.append([4, 8, 16].index(params[1]))

        if params[2] not in [32, 64, 128]:
            raise AttributeError('param 6')
        else:
            idx.append([32, 64, 128].index(params[2]))
    
    else:
        raise AttributeError('params length should be 3 or 5')

    return tuple(idx)
    

if __name__ == '__main__':
    cpi = np.zeros(shape=(4, 3, 4, 3, 3))

    for benchmark in os.listdir('xplore-1/'):
        for params in os.listdir('xplore-1/' + benchmark):
            # Current expirement

            with open('xplore-1/{}/{}/stats.txt'.format(benchmark, params)) as f:
                params = split_name(params)
                params = params[0:4] + [params[6]]

                # Get CPI from stats.txt
                for i, line in enumerate(f):
                    if i == 28:
                        cpi[get_index(params)] += float(line.split()[1])
                        break

    np.save('l1.npy', cpi/5.0)

    l1 = cpi/5.0

    # i-cache
    plt.figure(1, figsize=(10.2, 4.8))

    plt.subplot(1, 2, 1)
    plt.plot(np.mean(l1, axis=(1, 2, 3, 4)))
    plt.xlabel('i-cache size')
    plt.ylabel('average CPI')
    plt.xticks([0, 1, 2, 3], labels=['16 KB', '32 KB', '64 KB', '128 KB'])

    plt.subplot(1, 2, 2)
    plt.plot(np.mean(l1, axis=(0, 2, 3, 4)))
    plt.xlabel('i-cache assoc.')
    plt.xticks([0, 1, 2], labels=[1, 2, 4])

    plt.suptitle('I-Cache')
    plt.savefig('img/i-cache.jpg')
    plt.show()

    # d-cache
    plt.close(fig=plt.gcf())
    plt.figure(2, figsize=(10.2, 4.8))

    plt.subplot(1, 2, 1)
    plt.plot(np.mean(l1, axis=(0, 1, 3, 4)))
    plt.xlabel('d-cache size')
    plt.ylabel('average CPI')
    plt.xticks([0, 1, 2, 3], labels=['16 KB', '32 KB', '64 KB', '128 KB'])

    plt.subplot(1, 2, 2)
    plt.plot(np.mean(l1, axis=(0, 1, 2, 4)))
    plt.xlabel('d-cache assoc.')
    plt.xticks([0, 1, 2], labels=[2, 4, 8])

    plt.suptitle('D-Cache')
    plt.savefig('img/d-cache.jpg')
    plt.show()

    # Cache line size
    plt.plot(np.mean(l1, axis=(0, 1, 2, 3)))
    plt.xlabel('cache line size')
    plt.ylabel('average CPI')
    plt.xticks([0, 1, 2], labels=[32, 64, 128])

    plt.title('Cache Line')
    plt.savefig('img/l1-cache-line.jpg')
    plt.show()

    cpi = np.zeros(shape=(5, 3, 3))

    for benchmark in os.listdir('xplore-2/'):
        for params in os.listdir('xplore-2/' + benchmark):
            # Current expirement

            with open('xplore-2/{}/{}/stats.txt'.format(benchmark, params)) as f:
                params = split_name(params)
                params = params[4:]

                # Get CPI from stats.txt
                for i, line in enumerate(f):
                    if i == 28:
                        cpi[get_index(params)] += float(line.split()[1])
                        break

    np.save('l2.npy', cpi/5)

    l2 = cpi/5.0

    # l2-cache
    plt.close(fig=plt.gcf())
    plt.figure(3, figsize=(10.2, 4.8))

    plt.subplot(1, 2, 1)
    plt.plot(np.mean(l2, axis=(1, 2)))
    plt.xlabel('l2-cache size')
    plt.ylabel('average CPI')
    plt.xticks([0, 1, 2, 3, 4], labels=['256 KB', '512 KB', '1 MB', '2 MB', '4 MB'])

    plt.subplot(1, 2, 2)
    plt.plot(np.mean(l2, axis=(0, 2)))
    plt.xlabel('l2-cache assoc.')
    plt.xticks([0, 1, 2], labels=[4, 8, 16])

    plt.suptitle('L2-Cache')
    plt.savefig('img/l2-cache.jpg')
    plt.show()

    # Cache line size
    plt.plot(np.mean(l2, axis=(0, 1)))
    plt.xlabel('cache line size')
    plt.ylabel('average CPI')
    plt.xticks([0, 1, 2], labels=[32, 64, 128])

    plt.title('Cache Line')
    plt.savefig('img/l2-cache-line.jpg')
    plt.show()