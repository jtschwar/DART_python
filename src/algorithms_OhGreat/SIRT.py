import astra

def SIRT(vol_geom, vol_data, sino_id, iters=2000, use_gpu=False, min_constraint=0, max_constraint=255):
        # create starting reconstruction
        rec_id = astra.data2d.create('-vol', vol_geom, data=vol_data)
        # define SIRT config params
        alg_cfg = astra.astra_dict('SIRT_CUDA' if use_gpu else 'SIRT')
        alg_cfg['ProjectionDataId'] = sino_id
        alg_cfg['ReconstructionDataId'] = rec_id
        alg_cfg['option'] = {}
        alg_cfg['option']['MinConstraint'] = min_constraint
        alg_cfg['option']['MaxConstraint'] = max_constraint
        # define algorithm
        alg_id = astra.algorithm.create(alg_cfg)
        # run the algorithm
        astra.algorithm.run(alg_id, iters)
        # create reconstruction data
        rec = astra.data2d.get(rec_id)

        return rec_id, rec